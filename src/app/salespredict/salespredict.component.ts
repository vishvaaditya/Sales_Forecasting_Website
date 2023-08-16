import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { FormBuilder} from '@angular/forms';
import { Router } from '@angular/router';

@Component({
  selector: 'app-salespredict',
  templateUrl: './salespredict.component.html',
  styleUrls: ['./salespredict.component.css']
})
export class SalespredictComponent implements OnInit {

  @ViewChild('fileSelect') myInputVariable?: ElementRef;
  
  

  filename: any;
  format: any;
  formfile: any;
  file:any;
  


  constructor(
    private http: HttpClient,
    private router: Router,
    ) {}

  ngOnInit(): void {}


  onFileSelect(event: any) {
    try {
       this.file = event.target.files[0];
      if (this.file) {
        this.filename = this.file.name;
        this.format = this.file.name.split('.');
        // this.format = this.format[1];
        if (this.format[1] != 'csv') {
          alert("provide csv file!!!")
          this.deleteFile();
        } else {
          this.formfile = new FormData();
          this.formfile.append('file', this.file);
          console.log("file is in correct format", this.formfile);
        }
      }
    } catch (error) {
      this.deleteFile();
      console.log('no file was selected...');
    }
  }
  fileUpload() {
    if (this.file) {
     
      let url = "http://127.0.0.1:5000/api/file_upload"
      this.http.post(url, this.formfile).subscribe((res) => {
      alert("file uploaded sucessfully!!!");
      },
        (error) => {
          alert("close!")
        });
    }
  }
  deleteFile(){
    this.file = null;
    this.format = null;
    this.filename = null;
    this.formfile.delete('file');
    // this.fileSelect
  }
}



