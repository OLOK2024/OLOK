import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import {BehaviorSubject, Observable, tap} from 'rxjs';
import { throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = 'http://localhost:8000/api'; // remplacez par l'URL de votre API
  private currentUserSubject = new BehaviorSubject<any>(null);
  public currentUser = this.currentUserSubject.asObservable();

  constructor(private http: HttpClient) { }

  login(email: string, password: string): Observable<any> {
    const credentials = { email, password };
    return this.http.post<any>(`${this.apiUrl}/auth/login`, credentials).pipe(
      tap(user => this.setCurrentUser(user)),
      catchError(error => {
        // gérer l'erreur d'authentification ici
        if (error.status === 401) {
          // renvoyer une erreur appropriée à l'utilisateur
          return throwError('E-mail ou mot de passe incorrect');
        } else {
          // renvoyer l'erreur telle quelle
          return throwError(error);
        }
      })
    );
  }


  signUp(email: string, firstName: string, lastName: string, country: string, startTime: string, endTime: string, workDays: number, password: string, passwordConfirmed: string): Observable<any> {
    const user = { email, firstName, lastName, password, passwordConfirmed, startTime, endTime, workDays, country};
    return this.http.post<any>(`${this.apiUrl}/auth/signup`, user).pipe(
      // enregistrez les informations de l'utilisateur connecté dans le service
      tap(user => this.setCurrentUser(user))
    );
  }

  logout(): void {
    // supprimez les informations de l'utilisateur connecté du service
    this.currentUserSubject.next(null);
  }

  private setCurrentUser(user: any): void {
    // stockez les informations de l'utilisateur connecté dans le service
    this.currentUserSubject.next(user);
  }
}
