import { Component, OnInit } from '@angular/core';
import { ProductService } from 'src/app/services/product.service';
import { Product } from 'src/app/models/product';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  products: Product[] = [];

  constructor(private productService:ProductService) { }

  ngOnInit(): void {
    this.productService.getProduct().subscribe((product) => (this.products = product))
    console.log(this.products)
  }

}
