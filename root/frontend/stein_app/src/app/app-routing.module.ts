import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { CommentComponent } from './comment/comment.component';
import { HomeComponent } from './home/home.component';
import { LoginComponent } from './login/login.component';
import { RegistrationComponent } from './registration/registration.component';

const routes: Routes = [
  { path: 'login', component: LoginComponent },
  { path: 'registration', component: RegistrationComponent },
  { path: '', component: HomeComponent },
  // { path: 'profile/:name', component: ProfileComponent },
  // { path: 'post/:id', component: PostBigComponent },
  // { path: 'support', component: SupportComponent },
  // Testing routes
  // { path: 'postsmall', component: PostSmallComponent },
  { path: 'comment', component: CommentComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
