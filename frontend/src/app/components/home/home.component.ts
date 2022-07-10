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

  list!: Item;
  id:number;

  constructor(private productService: ProductService) { 
    this.list.id = this.id;
  }

  ngOnInit(): void {
    this.productService.GetData().subscribe((item) => {
      console.log(item);
      this.list = item;
    })
    this.productService.GetDatabyId(this.list.id).subscribe((item) => {
      console.log(item);
    // this.router.navigate(['/product'])
    })

    // this.productService.GetData().subscribe((item) => {
    //   console.log(item);
    //   this.list = item;
    // })
  }
  // goToUrl(id:number){
  //   this.productService.GetDatabyId(id).subscribe((item) => {
  //     console.log(item);
  //   // this.router.navigate(['/product'])
  //   })
  }

// }
