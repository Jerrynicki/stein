import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { BrowserModule } from '@angular/platform-browser';

import { HttpClientModule } from '@angular/common/http';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HomeComponent } from './home/home.component';
import { LoginComponent } from './login/login.component';
import { PostSmallComponent } from './post-small/post-small.component';
import { RegistrationComponent } from './registration/registration.component';

import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatIconModule } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { MatListModule } from '@angular/material/list';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatSelectModule } from '@angular/material/select';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatToolbarModule } from '@angular/material/toolbar';
import { CommentComponent } from './comment/comment.component';

import { DividerModule } from 'primeng/divider';
import { FileUploadModule } from 'primeng/fileupload';
import { InputNumberModule } from 'primeng/inputnumber';
import { ImageModule } from 'primeng/image';
import { InputTextModule } from 'primeng/inputtext';
import { RatingModule } from 'primeng/rating';
import { SidebarModule } from 'primeng/sidebar';
import { AvatarModule } from 'primeng/avatar';
import { InputSwitchModule } from 'primeng/inputswitch';
import { CreateComponent } from './create/create.component';
import { ImpressumComponent } from './impressum/impressum.component';
import { PostBigComponent } from './post-big/post-big.component';
import { ProfileComponent } from './profile/profile.component';
import { SupportComponent } from './support/support.component';
import { ToolbarComponent } from './toolbar/toolbar.component';

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    RegistrationComponent,
    PostSmallComponent,
    HomeComponent,
    CommentComponent,
    ProfileComponent,
    PostBigComponent,
    SupportComponent,
    ImpressumComponent,
    CreateComponent,
    ToolbarComponent,
  ],
  imports: [
    BrowserModule,
    FormsModule,
    AppRoutingModule,
    HttpClientModule,
    BrowserAnimationsModule,
    MatButtonModule,
    MatFormFieldModule,
    MatIconModule,
    MatInputModule,
    MatProgressSpinnerModule,
    MatSelectModule,
    MatCardModule,
    MatToolbarModule,
    MatSidenavModule,
    MatListModule,
    RatingModule,
    SidebarModule,
    DividerModule,
    FileUploadModule,
    InputTextModule,
    ImageModule,
    AvatarModule,
    InputSwitchModule,
    InputNumberModule,
  ],
  providers: [],
  bootstrap: [AppComponent],
})
export class AppModule {}
