import { Injectable } from '@angular/core';
import { HttpEvent, HttpInterceptor, HttpHandler, HttpRequest } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable()
export class TokenInterceptor implements HttpInterceptor {
  intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    // récupère le token JWT du localStorage
    const token = localStorage.getItem('token');
    console.log(token);

    // vérifie si le token existe
    if (token) {
      // clone la requête et ajoute le token dans l'en-tête Authorization
      request = request.clone({
        setHeaders: {
          Authorization: `Bearer ${token}`
        }
      });
    }

    // transmet la requête modifiée ou originale
    return next.handle(request);
  }
}
