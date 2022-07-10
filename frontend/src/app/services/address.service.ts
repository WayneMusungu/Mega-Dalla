import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment';
import { Address } from '../models/address';

@Injectable({
  providedIn: 'root'
})
export class AddressService {

  private url = `${environment.apiUrl}`;

  constructor(private http: HttpClient) { }

  checkoutdata(address: Address ){
    return this.http.post<Address>(`${this.url}/address/`,address);
    
  }

  
}
