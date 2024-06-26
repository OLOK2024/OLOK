import { HttpInterceptorFn } from '@angular/common/http';

export const tokenInterceptor: HttpInterceptorFn = (req, next) => {
  // récupère le token JWT du localStorage

  try {
    const token = localStorage.getItem('token');
    console.log(token);
    // vérifie si le token existe
    if (token && token != "undefined") {
      // clone la requête et ajoute le token dans l'en-tête Authorization
      const newReq = req.clone({
        headers: req.headers.set('Authorization', `Bearer ${token}`),
      });
      return next(newReq);
  }
  } catch (error) {
    console.error('Error getting token from localStorage:', error);
  }

  // transmet la requête modifiée ou originale
  return next(req);
}
