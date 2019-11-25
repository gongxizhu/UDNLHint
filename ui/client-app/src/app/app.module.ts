import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { LoadingComponent } from './core/components/loading/loading.component';
import { CreateOrderComponent } from './modules/order/components/create-order/create-order.component';
import { OrderModule } from './modules/order/order.module';
import { CoreModule } from 'src/app/core/core.module';
import { OrderService } from './modules/order/services/order.service';


@NgModule({
  declarations: [
    AppComponent
    // LoadingComponent,
    //CreateOrderComponent
  ],
  imports: [
    CommonModule,
    BrowserAnimationsModule,
    BrowserModule,
    AppRoutingModule,
    CoreModule,
    OrderModule
  ],
  providers: [OrderService],
  bootstrap: [AppComponent]
})
export class AppModule { }
