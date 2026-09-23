import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: '',
    loadComponent: () => import('./pages/home/home').then(m => m.Home),
  },
  {
    path: 'matches',
    loadComponent: () => import('./pages/matches/matches').then(m => m.Matches),
  },
  {
    path: 'matches/:id',
    loadComponent: () => import('./pages/matches/matches').then(m => m.Matches),
  },
  {
    path: 'players',
    loadComponent: () => import('./pages/player-breakdown/player-breakdown').then(m => m.PlayerBreakdown),
  },
  {
    path: 'players/:id',
    loadComponent: () => import('./pages/player-breakdown/player-breakdown').then(m => m.PlayerBreakdown),
  },
  { path: '**', redirectTo: '' },
];
