import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PlayerBreakdown } from './player-breakdown';

describe('PlayerBreakdown', () => {
  let component: PlayerBreakdown;
  let fixture: ComponentFixture<PlayerBreakdown>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PlayerBreakdown],
    }).compileComponents();

    fixture = TestBed.createComponent(PlayerBreakdown);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
