import {Component, OnInit} from '@angular/core';
import {ActivatedRoute, Router} from '@angular/router';
import {ApiService} from '../api.service';
import {FormBuilder,FormGroup, NgForm, Validators} from '@angular/forms';

@Component({
  selector: 'app-book-edit',
  templateUrl: './book-edit.component.html',
  styleUrls: ['./book-edit.component.css']
})
export class BookEditComponent implements OnInit {

  bookForm: FormGroup;



  book :any= {};

  constructor(private router: Router, private route: ActivatedRoute, private api: ApiService, private formBuilder: FormBuilder) {
  }

  ngOnInit() {
    this.bookForm = this.formBuilder.group({
      'isbn': [null, Validators.required],
      'title': [null, Validators.required],
      'description': [null, Validators.required],
      'author': [null, Validators.required],
      'publisher': [null, Validators.required],
      'published_year': [null, Validators.required]
    });

    this.getBookDetails(this.route.snapshot.params['id']);
  }

  getBookDetails(id) {
    this.api.getBook(id)
      .subscribe(data => {
        console.log(data);
        this.book = data;
        console.log(this.book.isbn);
        this.bookForm = this.formBuilder.group({
          'isbn': [this.book.isbn, Validators.required],
          'title': [this.book.title, Validators.required],
          'description': [this.book.description, Validators.required],
          'author': [this.book.author, Validators.required],
          'publisher': [this.book.publisher, Validators.required],
          'published_year': [this.book.published_year, Validators.required]
        });
      });
  }

  onFormSubmit(form: NgForm) {
    let id = this.route.snapshot.params['id'];
    this.api.updateBook(id,form)
      .subscribe(res => {
        console.log(res);
        let id = res['_id'];
        this.router.navigate(['/book-details', id]);
      }, (err) => {
        console.log(err);
      });
  }

}
