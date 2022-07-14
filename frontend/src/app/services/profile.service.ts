import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';
import { Profile } from '../models/profile';

@Injectable({
  providedIn: 'root'
})
export class ProfileService {

  private url = `${environment.apiUrl}`;

  constructor(private http: HttpClient) { }


  upDate(profile:any ): Observable<any>{
    return this.http.patch(`${this.url}/profile/`,profile);
    
  }
}
