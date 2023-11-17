import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ToolbarUiComponent } from './toolbar-ui.component';

describe('ToolbarUiComponent', () => {
  let component: ToolbarUiComponent;
  let fixture: ComponentFixture<ToolbarUiComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ToolbarUiComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ToolbarUiComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
