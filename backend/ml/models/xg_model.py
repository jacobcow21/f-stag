"""
Expected Goals (xG) model.

Plan:
  v1 — Logistic regression baseline: distance, angle, body part, situation
  v2 — XGBoost with spatial features: freeze frame (defenders in lane),
        shot technique, preceding action type/distance, game state

Input:  Shot event DataFrame (one row per shot)
Output: xG probability per shot [0.0, 1.0]
"""
