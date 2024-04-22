import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import {Observable} from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class KeyService {
  private apiUrl = 'http://localhost:8000/api';

  constructor(private http: HttpClient) { }

  getPasswordKeys(): Observable<any> {
    return this.http.get<any[]>(`${this.apiUrl}/bunchOfKeys`);
  }

  addPasswordKey(key: any): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/key/`, key);
  }
}
