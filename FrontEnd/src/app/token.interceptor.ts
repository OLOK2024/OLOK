import { HttpInterceptorFn } from '@angular/common/http';

export const tokenInterceptor: HttpInterceptorFn = (req, next) => {
  // récupère le token JWT du localStorage
  const token = localStorage.getItem('token');
  console.log(token);

  // vérifie si le token existe
  if (token) {
    // clone la requête et ajoute le token dans l'en-tête Authorization
    const newReq = req.clone({
      headers: req.headers.set('Authorization', `Bearer ${token}`),
    });
    return next(newReq);
  }

  // transmet la requête modifiée ou originale
  return next(req);
}
