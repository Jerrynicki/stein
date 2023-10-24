import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { CommentComponent } from './comment/comment.component';
import { CreateComponent } from './create/create.component';
import { HomeComponent } from './home/home.component';
import { ImpressumComponent } from './impressum/impressum.component';
import { LoginComponent } from './login/login.component';
import { PostBigComponent } from './post-big/post-big.component';
import { ProfileComponent } from './profile/profile.component';
import { RegistrationComponent } from './registration/registration.component';
import { SupportComponent } from './support/support.component';
import { ToolbarComponent } from './toolbar/toolbar.component';

const routes: Routes = [
  { path: 'login', component: LoginComponent },
  { path: 'registration', component: RegistrationComponent },
  { path: '', component: HomeComponent },
  { path: 'profile/:name', component: ProfileComponent },
  { path: 'post/:id', component: PostBigComponent },
  { path: 'create', component: CreateComponent },
  { path: 'support', component: SupportComponent },
  { path: 'impressum', component: ImpressumComponent },
  // Testing routes
  // { path: 'postsmall', component: PostSmallComponent },
  { path: 'comment', component: CommentComponent },
  { path: 'toolbar', component: ToolbarComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
