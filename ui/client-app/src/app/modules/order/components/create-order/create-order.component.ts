import { Component, OnInit } from '@angular/core';
import { KendoGridSetting } from '../../kendo-grid-setting';
import { PageChangeEvent } from '@progress/kendo-angular-grid';
import { SortDescriptor } from '@progress/kendo-data-query';
import { OrderService } from '../../services/order.service';
import { Orderline } from '../../orderline';

@Component({
  selector: 'app-create-order',
  templateUrl: './create-order.component.html',
  styleUrls: ['./create-order.component.less']
})
export class CreateOrderComponent implements OnInit {

  displayLoader: boolean;
  orderlines: Orderline[];
  lastNote: string;
  lastChassis: string;
  constructor(private orderApi: OrderService) { }
  gridSetting: KendoGridSetting = new KendoGridSetting();
  get dsSalesTypes() {
    return [
      { value: 1, item: 'Heavy Duty Truck' },
      { value: 2, item: 'Medium Duty Truck' },
      { value: 3, item: 'Light Duty Truck' },
      { value: 7, item: 'Trailor' },
      { value: 9, item: 'Others' }
      ];
  }
  get dsServiceType() {
    return [
      { value: 1, item: 'General Service' },
      { value: 2, item: 'Shaken' },
      { value: 3, item: 'P I' },
      { value: 4, item: 'Accident' },
      ];
  }
  get dsOrderlines() {
    return this.orderlines;
  }
  ngOnInit() {
  }

  onSubmit() {
    this.onSearchClick();
  }
  onSearchClick() {
    this.search();
  }
  onChassisFocusOut() {
    const noteTag = <HTMLInputElement>document.getElementById('note');
    const chassisTag = <HTMLInputElement>document.getElementById('chassis');
    const note = noteTag.value.trim();
    const chassis = chassisTag.value.trim();
    if ( note === '') {
      return;
    }
    if ( this.lastNote === note && this.lastChassis === chassis) {
      return;
    }
    this.displayLoader = true;
    this.lastNote = note;
    this.lastChassis = chassis
    this.orderApi.getOrderlines(note, chassis).subscribe(res => {
      const answer: Orderline[] = res;
      console.log(answer);
      this.orderlines = answer;
      this.displayLoader = false;
    });
  }
  onNoteFocusOut() {
    const noteTag = <HTMLInputElement>document.getElementById('note');
    const chassisTag = <HTMLInputElement>document.getElementById('chassis');
    const note = noteTag.value.trim();
    const chassis = chassisTag.value.trim();
    if ( note === '') {
      return;
    }
    if ( this.lastNote === note && this.lastChassis === chassis) {
      return;
    }
    this.displayLoader = true;
    this.lastNote = note;
    this.lastChassis = chassis
    this.orderApi.getOrderlines(note, chassis).subscribe(res => {
      const answer: Orderline[] = res;
      console.log(answer);
      this.orderlines = answer;
      this.displayLoader = false;
    });
  }
  async search() {
    await this.getOrderlines();
  }
  async getOrderlines() {
    //const result = await this.orderService.getOrderlines('service type', 'chassis', 'notes').toPromise();
    //this.gridSetting.data = { data: result.data, total: result.total };
  }
}
