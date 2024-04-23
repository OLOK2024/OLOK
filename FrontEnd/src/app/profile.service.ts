import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ProfileService {

  private apiUrl = 'http://localhost:8000/api';

  constructor(private http: HttpClient) { }

  getProfile(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/profile/`);
  }

  deleteProfile(): Observable<any[]> {
    return this.http.delete<any>(`${this.apiUrl}/profile/`);
  }

  updateProfileInfo(first_name: string, last_name: string, country_code: string, start_of_day: string, end_of_day: string, workdays: string): Observable<any> {
    const profileInfo = { first_name, last_name, country_code, start_of_day, end_of_day, workdays};
    return this.http.put<any>(`${this.apiUrl}/profile/`, profileInfo);
  }

  updatePassword(old_password: string, new_password: string, confirm_new_password: string): Observable<any> {
    const newPassword = { old_password, new_password, confirm_new_password };
    return this.http.put<any>(`${this.apiUrl}/profile/change_password/`, newPassword);
  }
}
