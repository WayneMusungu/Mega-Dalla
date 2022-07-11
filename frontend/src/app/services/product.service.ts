import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http'
import {Observable} from 'rxjs';
import { Product } from '../models/product';

@Injectable({
  providedIn: 'root'
})
export class ProductService {
  private apiUrl = 'http://localhost:8000/api/items'

  constructor(private http:HttpClient) { }

  getProduct(): Observable<Product[]> {
    return this.http.get<Product[]>(this.apiUrl)
  }
}
