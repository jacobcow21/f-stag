import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: '',
    loadComponent: () => import('./pages/home/home').then(m => m.HomeComponent),
  },
  {
    path: 'matches',
    loadComponent: () => import('./pages/matches/matches').then(m => m.MatchesComponent),
  },
  {
    path: 'matches/:id',
    loadComponent: () => import('./pages/matches/matches').then(m => m.MatchesComponent),
  },
  {
    path: 'players',
    loadComponent: () => import('./pages/player-breakdown/player-breakdown').then(m => m.PlayerBreakdownComponent),
  },
  {
    path: 'players/:id',
    loadComponent: () => import('./pages/player-breakdown/player-breakdown').then(m => m.PlayerBreakdownComponent),
  },
  { path: '**', redirectTo: '' },
];
