import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import {Observable} from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class KeyService {
  private apiUrl = 'http://localhost:8000/api';

  constructor(private http: HttpClient) { }

  addPasswordKey(key: any): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/key/`, key);
  }

  getPassword(bunchOfKeysId: string, keyId: string): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/key/password/${bunchOfKeysId}/${keyId}/`);
  }

  deleteKey(bunchOfKeysId: string, keyId: string): Observable<any> {
    return this.http.delete<any>(`${this.apiUrl}/key/del/${bunchOfKeysId}/${keyId}/`);
  }
}
