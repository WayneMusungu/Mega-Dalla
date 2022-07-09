import { Component, OnInit } from '@angular/core';
import { Item } from 'src/app/models/product';
import { ProductService } from 'src/app/services/product.service';

@Component({
  selector: 'app-product',
  templateUrl: './product.component.html',
  styleUrls: ['./product.component.css']
})
export class ProductComponent implements OnInit {

  item!: Item;
  constructor(private productService: ProductService) { }

  ngOnInit(): void {

    this.productService.GetData().subscribe((item) => {
      console.log(item);
      this.item = item;
    })
  }

}
