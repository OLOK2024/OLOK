import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import {Injectable} from "@angular/core";

@Injectable({
  providedIn: 'root'
})
export class BunchOfKeysService {
  private apiUrl = 'http://localhost:8000/api';

  constructor(private http: HttpClient) { }

  getBunchOfKeys(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/bunchOfKeys/`);
  }

  createBunchOfKey(name: string, description: string): Observable<any> {
    const bunchOfKey = { name, description };
    return this.http.post<any>(`${this.apiUrl}/bunchOfKeys/`, bunchOfKey);
  }

  updateBunchOfKey(bunchOfKeysId: string, name: string, description: string): Observable<any> {
    const bunchOfKey = { name, description };
    return this.http.put<any>(`${this.apiUrl}/bunchOfKeys/${bunchOfKeysId}/`, bunchOfKey);
  }

  deleteBunchOfKey(bunchOfKeysId: string): Observable<any> {
    return this.http.delete<any>(`${this.apiUrl}/bunchOfKeys/${bunchOfKeysId}/`);
  }
}
