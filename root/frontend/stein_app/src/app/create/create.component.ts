import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { GeolocationService } from '@ng-web-apis/geolocation';
import { CreateInterface } from './create.interface';

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

    this.geolocation.subscribe((position) => {
      this.lat = position.coords.latitude;
      this.lng = position.coords.longitude;
    });
  }

  login: boolean = false;
  imageaccept: boolean = false;
  uploadedFile: any;
  lat: number = 0;
  lng: number = 0;
  b64: string = '';
  id: number = 0;

  httpOptions = {
    headers: new HttpHeaders({
      'Content-Type': 'application/json',
      Authorization: 'Bearer' + sessionStorage.getItem('token'),
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
    const b64formatted = this.b64.split(',')[1];
    console.log(b64formatted);
    this.http
      .post<{id: number}>(
        'http://localhost:5000/api/post',
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
          this.router.navigate([
            '/post',
            this.id,
          ]);
        },
      });
  }
}
