import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CommentUiComponent } from './comment-ui.component';

describe('CommentUiComponent', () => {
  let component: CommentUiComponent;
  let fixture: ComponentFixture<CommentUiComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CommentUiComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(CommentUiComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
