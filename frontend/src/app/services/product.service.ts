import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';
import { Item } from '../models/product';

@Injectable({
  providedIn: 'root'
})
export class ProductService {

  private url = `${environment.apiUrl}`;
  

  constructor(private http: HttpClient) { }

  GetData(): Observable<Item> {
    return this.http.get<Item>(`${this.url}/items`);
  }

}
