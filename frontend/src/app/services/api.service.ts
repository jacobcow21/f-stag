import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

import { environment } from '../../environments/environment';

export interface Match {
  match_id: number;
  match_date: string;
  kick_off: string;
  match_week: number;
  home_team: string;
  home_team_id: number;
  home_score: number;
  away_team: string;
  away_team_id: number;
  away_score: number;
  stadium: string;
  competition_name: string;
  season: string;
}

export interface EventSummary {
  total_events: number;
  shots: number;
  passes: number;
  carries: number;
  dribbles: number;
  pressures: number;
}

export interface MatchDetail {
  match: Match;
  event_summary: EventSummary;
}

export interface Player {
  player_id: number;
  player: string;
  team: string;
  event_count: number;
}

export interface PlayerStats {
  shots: number;
  goals: number;
  passes: number;
  key_passes: number;
  dribbles_completed: number;
}

export interface PlayerDetail {
  player_id: number;
  player: string;
  team: string;
  stats: PlayerStats;
}

@Injectable({ providedIn: 'root' })
export class ApiService {
  private http = inject(HttpClient);
  private base = environment.apiUrl;

  getMatches(): Observable<Match[]> {
    return this.http.get<{ matches: Match[] }>(`${this.base}/matches/`).pipe(
      map(r => r.matches)
    );
  }

  getMatch(id: number): Observable<MatchDetail> {
    return this.http.get<MatchDetail>(`${this.base}/matches/${id}`);
  }

  getPlayers(): Observable<Player[]> {
    return this.http.get<{ players: Player[] }>(`${this.base}/players/`).pipe(
      map(r => r.players)
    );
  }

  getPlayer(id: number): Observable<PlayerDetail> {
    return this.http.get<PlayerDetail>(`${this.base}/players/${id}`);
  }
}
