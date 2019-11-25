import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { HttpHeaders } from '@angular/common/http';
import { HttpErrorResponse } from '@angular/common/http';
import { Observable } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { Orderline } from '../orderline';

const httpOptions = {
    headers: new HttpHeaders({
        'Content-Type':  'application/json'
    })
};

export const API_URL = 'http://localhost:5000';

@Injectable()
export class OrderService {
    orderlinesAPIUrl = '/getorderlines';
    vehicleAPIUrl = '/getvehicle';
    constructor(private http: HttpClient) {

    }
    getVehicle(chassis: string): Observable<String> {
        return this.http.post(API_URL + this.vehicleAPIUrl, chassis, httpOptions) as Observable<String>;
    }
    getOrderlines(note: string, chassis: string): Observable<Orderline[]> {
        const params = new HttpParams()
        .set('note', note)
        .set('chassis', chassis);
        //return new Observable('tested');
        return this.http.post(API_URL + this.orderlinesAPIUrl, params, httpOptions) as Observable<Orderline[]>;
    }
}
