import { HttpInterceptorFn } from '@angular/common/http';

export const tokenInterceptor: HttpInterceptorFn = (req, next) => {
  // récupère le token JWT du localStorage
  const token = localStorage.getItem('token');
  console.log(token);

  // vérifie si le token existe
  if (token) {
    // clone la requête et ajoute le token dans l'en-tête Authorization
    const newReq = req.clone({
      headers: req.headers.set('Authorization', `Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzEzNzM5Nzg0LCJpYXQiOjE3MTM3Mzk0ODQsImp0aSI6ImI4Zjk1Njg3Yjk0MDRhNmI4MGE0NzgxZGY4ODU1ZTFiIiwidXNlcl9pZCI6MX0.AWiqtuyGQsdgTfMJA0cwx3Zh2T_wTqEpq5BzHZ1k0AQ`),
    });
    return next(newReq);
  }

  // transmet la requête modifiée ou originale
  return next(req);
}
