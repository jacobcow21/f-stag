import { Component, OnInit, inject } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';

import { ApiService, Player, PlayerDetail } from '../../services/api.service';

@Component({
  selector: 'app-player-breakdown',
  imports: [CommonModule, RouterLink],
  templateUrl: './player-breakdown.html',
})
export class PlayerBreakdown implements OnInit {
  private route = inject(ActivatedRoute);
  private api = inject(ApiService);

  playerId: number | null = null;
  players: Player[] = [];
  detail: PlayerDetail | null = null;
  loading = false;
  error: string | null = null;

  ngOnInit() {
    const id = this.route.snapshot.paramMap.get('id');
    if (id) {
      this.playerId = +id;
      this.loadDetail(this.playerId);
    } else {
      this.loadList();
    }
  }

  private loadList() {
    this.loading = true;
    this.api.getPlayers().subscribe({
      next: data => { this.players = data; this.loading = false; },
      error: () => { this.error = 'Failed to load players.'; this.loading = false; },
    });
  }

  private loadDetail(id: number) {
    this.loading = true;
    this.api.getPlayer(id).subscribe({
      next: data => { this.detail = data; this.loading = false; },
      error: () => { this.error = 'Failed to load player.'; this.loading = false; },
    });
  }
}
