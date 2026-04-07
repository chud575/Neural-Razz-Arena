"""
Neural Razz Arena — Flask API Server

Arena-only server for testing trained Neural CFR models.
Uses the same Python game engine the model was trained on.

Port: 5060
"""

import os
import sys
import json
import time
import threading
from flask import Flask, request, jsonify

from networks import StrategyNetwork
from features import FEATURE_DIM
from opponents import preload_all

app = Flask(__name__)

# ─── Global State ───────────────────────────────────────────────────────────

_model: StrategyNetwork = None
_model_info: dict = {}
_running = False
_lock = threading.Lock()

# Progress tracking for long-running tests
_progress = {'current': 0, 'total': 0, 'phase': 'idle', 'current_hand': ''}


# ─── Model Loading ──────────────────────────────────────────────────────────

def _load_model(path: str) -> bool:
    global _model, _model_info
    import torch

    try:
        with open(path) as f:
            data = json.load(f)

        network = StrategyNetwork()
        layers = data.get('layerConfigs', [])
        sd = network.state_dict()
        for i, lc in enumerate(layers):
            sd[f'fc{i+1}.weight'] = torch.tensor(lc['weights'], dtype=torch.float32)
            sd[f'fc{i+1}.bias'] = torch.tensor(lc['biases'], dtype=torch.float32)
        network.load_state_dict(sd)
        network.eval()

        params = sum(p.numel() for p in network.parameters())
        meta = data.get('metadata', {})
        iters = meta.get('iterations', 0)

        _model = network
        _model_info = {
            'path': path,
            'filename': os.path.basename(path),
            'parameters': params,
            'layers': len(layers),
            'iterations': iters,
            'metadata': meta,
        }
        print(f"[Arena] Model loaded: {os.path.basename(path)} ({params:,} params, {iters:,} iterations)")
        return True
    except Exception as e:
        print(f"[Arena] Failed to load model: {e}")
        return False


# ─── Endpoints ──────────────────────────────────────────────────────────────

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'has_model': _model is not None})


@app.route('/api/model/load', methods=['POST'])
def model_load():
    data = request.json or {}
    path = data.get('path', '')
    if not path or not os.path.exists(path):
        return jsonify({'error': f'File not found: {path}'}), 400
    if _load_model(path):
        return jsonify({'status': 'loaded', **_model_info})
    return jsonify({'error': 'Failed to load model'}), 500


@app.route('/api/model/info', methods=['GET'])
def model_info():
    if _model is None:
        return jsonify({'loaded': False})
    return jsonify({'loaded': True, **_model_info})


def _save_hand_history(result, opponent, num_hands, hand_scope, single_hand):
    """Save hand histories to a timestamped file. Never overwrites."""
    histories = result.get('hand_histories', [])
    if not histories:
        return

    import datetime
    ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    scope_label = single_hand or hand_scope or 'all'
    filename = f"arena_{opponent}_{scope_label}_{num_hands}h_{ts}.txt"

    save_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'hand_histories')
    os.makedirs(save_dir, exist_ok=True)
    filepath = os.path.join(save_dir, filename)

    with open(filepath, 'w') as f:
        # Header
        f.write(f"{'='*60}\n")
        f.write(f"Neural Razz Arena — Hand History\n")
        f.write(f"{'='*60}\n")
        f.write(f"Opponent: {opponent}\n")
        f.write(f"Hands: {num_hands}\n")
        f.write(f"Scope: {scope_label}\n")
        f.write(f"Win Rate: {result.get('win_rate', 0)}%\n")
        f.write(f"BB/100: {result.get('bb_per_100', 0):+.1f}\n")
        f.write(f"Fold Rate: {result.get('fold_rate', 0)}%\n")
        f.write(f"SD Win Rate: {result.get('sd_win_rate', 0)}%\n")
        f.write(f"{'='*60}\n\n")

        # Hands
        for hh in histories:
            f.write(f"#{hh['hand_num']}  Hero: {hh['hero_start']}  vs  {hh['villain_door']}  →  {hh['result']}  {hh['payoff']:+.1f}\n")
            for action_line in hh.get('actions', []):
                f.write(f"    {action_line}\n")
            if not hh.get('hero_folded', False):
                f.write(f"    Final: Hero={hh.get('hero_final','?')} Opp={hh.get('villain_final','?')}\n")
            f.write("\n")

    print(f"[Arena] Hand history saved: {filepath} ({len(histories)} hands)")


@app.route('/api/arena/run', methods=['POST'])
def arena_run():
    global _running
    if _model is None:
        return jsonify({'error': 'No model loaded'}), 400
    if _running:
        return jsonify({'error': 'Test already running'}), 400

    data = request.json or {}
    opponent = data.get('opponent', 'pure_ev')
    num_hands = data.get('num_hands', 5000)
    hand_scope = data.get('hand_scope')
    single_hand = data.get('single_hand')

    _running = True
    try:
        from arena_test import run_arena
        print(f"[Arena] Running {num_hands:,} hands vs {opponent} (scope={hand_scope or 'all'}, single={single_hand or 'none'})")
        t0 = time.time()
        result = run_arena(_model, num_hands=num_hands, opponent_type=opponent,
                          hand_scope=hand_scope, single_hand=single_hand)
        elapsed = time.time() - t0
        print(f"[Arena] Complete: Win={result['win_rate']}% BB/100={result['bb_per_100']:+.1f} ({elapsed:.1f}s)")

        # Save hand history to file (never overwrite — use timestamp)
        _save_hand_history(result, opponent, num_hands, hand_scope, single_hand)

        return jsonify(result)
    finally:
        _running = False


@app.route('/api/arena/all-hands', methods=['POST'])
def arena_all_hands():
    """Run all 455 starting hand combos individually."""
    global _running
    if _model is None:
        return jsonify({'error': 'No model loaded'}), 400
    if _running:
        return jsonify({'error': 'Test already running'}), 400

    data = request.json or {}
    opponent = data.get('opponent', 'pure_ev')
    hands_per_combo = data.get('hands_per_combo', 100)

    _running = True
    try:
        from arena_test import run_arena
        from trainer_strategy import get_starting_hands

        # Get all 455 hands
        all_hands = get_starting_hands('allHands')

        # EV lookup for sorting/grouping
        from bucketer import hero_ev_percentile, classify_hero, RANK_CHARS, load_ev_tables
        load_ev_tables()

        print(f"[Arena] All Hands Test: {len(all_hands)} combos x {hands_per_combo} hands vs {opponent}")
        t0 = time.time()

        results = []
        for i, hand_ranks in enumerate(all_hands):
            hand_str = ''.join(RANK_CHARS.get(r, '?') for r in sorted(hand_ranks))
            r = run_arena(_model, num_hands=hands_per_combo, opponent_type=opponent,
                         single_hand=hand_str)

            ev = hero_ev_percentile(hand_ranks) * 100
            bucket = classify_hero(hand_ranks)

            results.append({
                'hand': hand_str,
                'bucket': bucket,
                'hands_played': r['num_hands'],
                'win_rate': r['win_rate'],
                'bb_per_100': r['bb_per_100'],
                'fold_rate': r['fold_rate'],
                'sd_win_rate': r['sd_win_rate'],
                'profit': r['total_profit'],
                'ev_pct': round(ev, 1),
                'delta': round(r['win_rate'] - ev, 1),
            })

            if (i + 1) % 50 == 0:
                print(f"  [{i+1}/{len(all_hands)}] hands tested...")

        # Sort by EV descending
        results.sort(key=lambda x: x['ev_pct'], reverse=True)

        # Compute totals
        total_hands = sum(r['hands_played'] for r in results)
        total_profit = sum(r['profit'] for r in results)
        total_wins = sum(r['hands_played'] * r['win_rate'] / 100 for r in results)
        overall_wr = total_wins / max(total_hands, 1) * 100
        overall_bb = (total_profit / 2.0) / max(total_hands / 100, 0.01)
        profitable = sum(1 for r in results if r['bb_per_100'] > 0)

        # EV group breakdown
        groups = [
            ('G1: Elite 70%+', 70, 100),
            ('G2: Strong 60-70%', 60, 70),
            ('G3: Good 50-60%', 50, 60),
            ('G4: Playable 45-50%', 45, 50),
            ('G5: Marginal 40-45%', 40, 45),
            ('G6: Weak 35-40%', 35, 40),
            ('G7: Bad 25-35%', 25, 35),
            ('G8: Trash <25%', 0, 25),
        ]
        ev_groups = []
        for name, lo, hi in groups:
            g_hands = [r for r in results if lo <= r['ev_pct'] < hi]
            if g_hands:
                g_total = sum(r['hands_played'] for r in g_hands)
                g_profit = sum(r['profit'] for r in g_hands)
                g_wins = sum(r['hands_played'] * r['win_rate'] / 100 for r in g_hands)
                g_wr = g_wins / max(g_total, 1) * 100
                g_bb = (g_profit / 2.0) / max(g_total / 100, 0.01)
                g_prof = sum(1 for r in g_hands if r['bb_per_100'] > 0)
                ev_groups.append({
                    'name': name,
                    'count': len(g_hands),
                    'win_rate': round(g_wr, 1),
                    'bb_per_100': round(g_bb, 1),
                    'profit': round(g_profit, 2),
                    'profitable': g_prof,
                })

        elapsed = time.time() - t0
        print(f"[Arena] All Hands Complete: BB/100={overall_bb:+.1f} Win={overall_wr:.1f}% Profitable={profitable}/{len(results)} ({elapsed:.0f}s)")

        return jsonify({
            'results': results,
            'total_hands': total_hands,
            'total_profit': round(total_profit, 2),
            'win_rate': round(overall_wr, 1),
            'bb_per_100': round(overall_bb, 2),
            'profitable_hands': profitable,
            'total_combos': len(results),
            'opponent': opponent,
            'hands_per_combo': hands_per_combo,
            'ev_groups': ev_groups,
            'elapsed_seconds': round(elapsed, 1),
        })
    finally:
        _running = False


@app.route('/api/battery', methods=['POST'])
def run_battery():
    if _model is None:
        return jsonify({'error': 'No model loaded'}), 400

    from battery_test import run_battery as _run_battery
    report = _run_battery(_model)

    results = []
    for r in report.results:
        results.append({
            'name': r.scenario.name,
            'tier': r.scenario.tier,
            'passed': r.passed,
            'predicted': r.predicted_action,
            'expected': r.scenario.expected_actions,
            'confidence': round(r.confidence * 100, 0),
            'probabilities': {k: round(v * 100, 0) for k, v in r.probabilities.items()},
        })

    return jsonify({
        'total': report.total_tests,
        'passed': report.total_passed,
        'score': round(report.score * 100, 0),
        'results': results,
        'tier_scores': {str(k): list(v) for k, v in report.tier_scores.items()},
    })


# ─── Startup ────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    print("=" * 50)
    print("  Neural Razz Arena Server v1.6")
    print("=" * 50)

    # Preload opponents
    preload_all()

    # Auto-load model if present
    model_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                               'neural_razz_strategy.json')
    if os.path.exists(model_path):
        _load_model(model_path)

    print(f"\n  Port: 5060")
    print(f"  Model: {'loaded' if _model else 'none'}")
    print()

    app.run(host='127.0.0.1', port=5060, debug=False, threaded=True)
