import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class ImageService {
  constructor() {}

  // Converts file into base64 string
  async toBase64(file: File): Promise<string> {
    const reader = new FileReader();
    let result: string = '';
    reader.readAsDataURL(file);
    reader.onload = () => {
      result = reader.result as string;
    };

    return result;
  }
}
