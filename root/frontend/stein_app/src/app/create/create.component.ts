import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { GeolocationService } from '@ng-web-apis/geolocation';
import { CreateInterface } from './create.interface';
import { ThemePalette } from '@angular/material/core';
import { ProgressSpinnerMode } from '@angular/material/progress-spinner';

@Component({
  selector: 'app-create',
  templateUrl: './create.component.html',
  styleUrls: ['./create.component.scss'],
})
export class CreateComponent implements OnInit {
  constructor(
    private readonly geolocation: GeolocationService,
    private http: HttpClient,
    public router: Router
  ) {}

  ngOnInit() {
    sessionStorage.getItem('login') == 'true'
      ? (this.login = true)
      : (this.login = false);
    if (!this.manualcoords && !this.locationloaded) {
      this.geolocation.subscribe((position) => {
        this.lat = position.coords.latitude;
        this.lng = position.coords.longitude;
        this.locationloaded = true;
      });
    }
  }

  hide = true;
  color: ThemePalette = 'warn';
  mode: ProgressSpinnerMode = 'indeterminate';
  value = 50;
  diameter = 50;

  login: boolean = false;
  loading: boolean = false;
  imageaccept: boolean = false;
  manualcoords: boolean = false;
  locationloaded: boolean = false;
  buttonpressed: boolean = false;
  uploadedFile: any;
  lat: number;
  manualLat: number;
  lng: number;
  manualLng: number;
  b64: string = '';
  id: number = 0;

  httpOptions = {
    headers: new HttpHeaders({
      'Content-Type': 'application/json',
      Authorization: 'Bearer ' + sessionStorage.getItem('token'),
    }),
  };

  onUpload(event: any) {
    const file: File = event.target.files[0];
    const image = new Image();
    image.src = URL.createObjectURL(file);

    image.onload = () => {
      const width = image.width;
      const height = image.height;

      if (width > height) {
        this.imageaccept = true;
      } else if (width < height) {
        this.imageaccept = false;
      } else {
        this.imageaccept = true;
      }

      const reader = new FileReader();

      reader.onload = (e: any) => {
        const base64String = e.target.result; // Hier erhalten Sie den Base64-String

        this.b64 = base64String;
        console.log(this.b64);
      };

      reader.readAsDataURL(file);
    };
  }

  async createPost() {
    this.buttonpressed = true
    this.loading = true
    const b64formatted = this.b64.split(',')[1];
    console.log(b64formatted);
    if (this.manualcoords) {
      this.lat = this.manualLat;
      this.lng = this.manualLng;
    }
    this.http
      .post<{id: number}>(
        '/api/post',
        {
          location_lat: this.lat,
          location_lon: this.lng,
          image: b64formatted,
        },
        this.httpOptions
      )
      .subscribe({
        next: (response) => {
          this.id = response.id
        },
        error: (error) => {
          console.error(error);
          if (error.status === 401) {
          } else {
          }
        },
        complete: () => {
          this.buttonpressed = false
          this.loading = false
          this.router.navigate([
            '/post',
            this.id,
          ]);
        },
      });
  }

  /* manualCoords(){
    if (this.manualcoords) {
      this.lat = 0
      this.lng = 0
    } else {
      this.geolocation.subscribe((position) => {
        this.lat = position.coords.latitude;
        this.lng = position.coords.longitude;
      });
    }
  } */
}
