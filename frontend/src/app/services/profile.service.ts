import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment';
import { Profile } from '../models/profile';

@Injectable({
  providedIn: 'root'
})
export class ProfileService {

  private url = `${environment.apiUrl}`;

  constructor(private http: HttpClient) { }


  upDate(profile: Profile ){
    return this.http.put<Profile>(`${this.url}/profile/`,profile);
    
  }
}
