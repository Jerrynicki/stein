export interface PostInterface {
    id: number;
    author: string;
    images: {quality_level: number,height: number,width:number, url: string}[];
    location_lat: number;
    location_lon: number;
    distance: number;
}
