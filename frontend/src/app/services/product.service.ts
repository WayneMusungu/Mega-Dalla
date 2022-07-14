import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { first, Observable } from 'rxjs';
import { environment } from 'src/environments/environment';
import { Item } from '../models/product';

@Injectable({
  providedIn: 'root'
})
export class ProductService {
  private apiUrl = 'http://localhost:8000/api/items'

  private url = `${environment.apiUrl}`;
  

  constructor(private http: HttpClient) { }

  GetData(): Observable<Item> {
    return this.http.get<Item>(`${this.url}/items`);
  }

  GetDatabyId(id:number): Observable<Item> {
    return this.http.get<Item>(`${this.url}/items/`+id);
  }
  getProduct(): Observable<Item[]> {
    return this.http.get<Item[]>(this.apiUrl)
  }
}
