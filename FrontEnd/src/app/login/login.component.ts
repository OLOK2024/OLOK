import { Component } from '@angular/core';
import { AuthService } from "../auth.service";
import { MatSnackBar } from '@angular/material/snack-bar';
import { Router } from "@angular/router";


@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  standalone: true,
  styleUrls: ['./login.component.css'],
  providers: [AuthService]
})

export class LoginComponent {
  constructor(private authService: AuthService, private snackBar: MatSnackBar, private router: Router) {}

  login() {
    const email = (document.getElementById('loginEmail') as HTMLInputElement).value;
    const password = (document.getElementById('loginPassword') as HTMLInputElement).value;
    this.authService.login(email, password).subscribe({
      next: () => {
        this.router.navigate(['/home']); // redirigez l'utilisateur vers la page d'accueil
      },
      error: (error) => {
        if (error.status === 401) {
          this.snackBar.open('Identifiants incorrects', 'Fermer', { duration: 3000 });
          console.error('Une ERREUR s\'est produite : ', error);
        } else {
          console.error('Une erreur s\'est produite : ', error);
        }
      }
    });
  }


  signUp() {
    const email = (document.getElementById('signInEmail') as HTMLInputElement).value;
    const firstName = (document.getElementById('signInFirstName') as HTMLInputElement).value;
    const lastName = (document.getElementById('signInLastName') as HTMLInputElement).value;
    const country = (document.getElementById('signInCountry') as HTMLSelectElement).value;
    const startTime = (document.getElementById('signInStartTime') as HTMLInputElement).value;
    const endTime = (document.getElementById('signInEndTime') as HTMLInputElement).value;
    const workDays = parseInt((document.getElementById('signInWorkDays') as HTMLInputElement).value);
    const password = (document.getElementById('signInPassword') as HTMLInputElement).value;
    const passwordConfirmed = (document.getElementById('signInPasswordConfirmed') as HTMLInputElement).value;
    this.authService.signUp(email, firstName, lastName, country, startTime, endTime, workDays, password, passwordConfirmed).subscribe({
      next: () => {
        // Réinitialisez les valeurs des champs à une chaîne vide
        (document.getElementById('signInEmail') as HTMLInputElement).value = '';
        (document.getElementById('signInFirstName') as HTMLInputElement).value = '';
        (document.getElementById('signInLastName') as HTMLInputElement).value = '';
        (document.getElementById('signInCountry') as HTMLSelectElement).value = '';
        (document.getElementById('signInStartTime') as HTMLInputElement).value = '';
        (document.getElementById('signInEndTime') as HTMLInputElement).value = '';
        (document.getElementById('signInWorkDays') as HTMLInputElement).value = '';
        (document.getElementById('signInPassword') as HTMLInputElement).value = '';
        (document.getElementById('signInPasswordConfirmed') as HTMLInputElement).value = '';

        this.router.navigate(['/login']); // redirigez l'utilisateur vers la page d'accueil
      },
      error: (error) => {
        this.snackBar.open(error, 'Close', { duration: 3000 }); // affichez le message d'erreur à l'utilisateur
      }
    });
  }
}
