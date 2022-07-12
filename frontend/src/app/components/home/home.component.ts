import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { Item } from 'src/app/models/product';
import { ProductService } from 'src/app/services/product.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  products: Item[] = [];

  list!: Item;
  id:number;

  constructor(private productService: ProductService) { }

  ngOnInit(): void {
    this.productService.GetData().subscribe((item) => {
      console.log(item);
      this.list = item;
    })

    this.productService.getProduct().subscribe((product) => (this.products = product))
    console.log(this.products)

  }

}