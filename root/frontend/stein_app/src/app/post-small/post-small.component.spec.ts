import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PostSmallComponent } from './post-small.component';

describe('PostSmallComponent', () => {
  let component: PostSmallComponent;
  let fixture: ComponentFixture<PostSmallComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [PostSmallComponent]
    });
    fixture = TestBed.createComponent(PostSmallComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
