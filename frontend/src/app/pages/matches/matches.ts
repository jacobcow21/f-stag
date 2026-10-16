import { Component, OnInit, inject } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';

import { ApiService, Match, MatchDetail } from '../../services/api.service';

@Component({
  selector: 'app-matches',
  imports: [CommonModule, RouterLink],
  templateUrl: './matches.html',
})
export class Matches implements OnInit {
  private route = inject(ActivatedRoute);
  private api = inject(ApiService);

  matchId: number | null = null;
  matches: Match[] = [];
  detail: MatchDetail | null = null;
  loading = false;
  error: string | null = null;

  ngOnInit() {
    const id = this.route.snapshot.paramMap.get('id');
    if (id) {
      this.matchId = +id;
      this.loadDetail(this.matchId);
    } else {
      this.loadList();
    }
  }

  private loadList() {
    this.loading = true;
    this.api.getMatches().subscribe({
      next: data => { this.matches = data; this.loading = false; },
      error: () => { this.error = 'Failed to load matches.'; this.loading = false; },
    });
  }

  private loadDetail(id: number) {
    this.loading = true;
    this.api.getMatch(id).subscribe({
      next: data => { this.detail = data; this.loading = false; },
      error: () => { this.error = 'Failed to load match.'; this.loading = false; },
    });
  }
}
