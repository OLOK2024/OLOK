import { Component } from '@angular/core';
import {Router, RouterOutlet} from '@angular/router';
import { LoginComponent } from './login/login.component';
import { HomeComponent } from './home/home.component';
import { ProfileComponent } from "./profile/profile.component";
import { HTTP_INTERCEPTORS } from '@angular/common/http';
import { HttpClientModule } from '@angular/common/http';
import { TokenInterceptor } from './token.interceptor';

@Component({
  selector: 'app-root',
  template: `
    <router-outlet></router-outlet>
  `,
  standalone: true,
  imports: [
    RouterOutlet,
    HttpClientModule
  ],
  styles: [],
  providers: [
    { provide: HTTP_INTERCEPTORS, useClass: TokenInterceptor, multi: true,},
  ]
})

export class AppComponent {
  constructor(private router: Router) {
    this.router.resetConfig([
      { path: '', redirectTo: '/login', pathMatch: 'full' },
      { path: 'login', component: LoginComponent },
      { path: 'home', component: HomeComponent },
      { path: 'profile', component: ProfileComponent}
      // Ajoutez d'autres routes selon vos besoins
    ]);
  }
}
