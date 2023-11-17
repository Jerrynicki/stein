import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PostUiComponent } from './post-ui.component';

describe('PostUiComponent', () => {
  let component: PostUiComponent;
  let fixture: ComponentFixture<PostUiComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PostUiComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(PostUiComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
