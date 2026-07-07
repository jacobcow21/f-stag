"""
Expected Threat (xT) / Possession Value model.

Plan:
  Grid-based approach: divide pitch into N×M zones, compute
  probability of scoring within K actions from each zone.
  Reference: Karun Singh (2019) xT methodology.

Input:  Pass/carry event DataFrame
Output: xT delta per action (value gained by moving ball from zone A → B)
"""
