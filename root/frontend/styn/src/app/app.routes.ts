import { Routes } from '@angular/router';
import { HomePageComponent } from './components/pages/home-page/home-page.component';
import { ToolbarUiComponent } from './components/lib/toolbar-ui/toolbar-ui.component';
import { NotfoundPageComponent } from './components/pages/notfound-page/notfound-page.component';

export const routes: Routes = [
  { path: '', component: HomePageComponent },
  { path: 'toolbar', component: ToolbarUiComponent },
  { path: '**', component: NotfoundPageComponent },
];
