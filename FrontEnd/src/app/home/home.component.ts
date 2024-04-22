import { Component, OnInit } from '@angular/core';
import {RouterLink} from "@angular/router";
import {KeyService} from "../key.service";
import {NgForOf} from "@angular/common";
import { ReactiveFormsModule, FormGroup, FormControl } from '@angular/forms';
import { BunchOfKeysService } from '../bunch-of-keys.service';
import { CommonModule } from "@angular/common";

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [
    RouterLink,
    NgForOf,
    ReactiveFormsModule,
    CommonModule
  ],
  templateUrl: './home.component.html',
  styleUrl: './home.component.css',
  providers: [KeyService]
})
export class HomeComponent implements OnInit {
  passwordKeys: any;
  addKeyForm = new FormGroup({
    domain: new FormControl('', []),
    username: new FormControl('', []),
    password: new FormControl('', []),
    bunchOfKeysId: new FormControl('', []),
  });
  bunchOfKeys: any[] = [];

  createBunchOfKeyModalForm = new FormGroup({
    name: new FormControl('', []),
    description: new FormControl('', []),
  });

  constructor(
    private keyService: KeyService,
    private bunchOfKeysService: BunchOfKeysService
  ) { }

  ngOnInit(): void {
    this.keyService.getPasswordKeys().subscribe({
      next: (keys) => {
        this.passwordKeys = keys;
      },
      error: (err) => {
        console.error('Error fetching password keys:', err);
      }
    });

    this.bunchOfKeysService.getBunchOfKeys().subscribe({
      next: (bunchOfKeys) => {
        this.bunchOfKeys = bunchOfKeys;
        console.log('Bunch of keys:', this.bunchOfKeys);
      },
      error: (err) => {
        console.error('Error fetching bunch of keys:', err);
      }
    });
  }

  onSubmit(): void {
    if (this.addKeyForm.valid) {
      this.keyService.addPasswordKey(this.addKeyForm.value).subscribe({
        next: (key) => {
          console.log('New key added:', key);
          this.passwordKeys.push(key);
          this.addKeyForm.reset();
        },
        error: (err) => {
          console.error('Error adding new key:', err);
        }
      });
    }
  }

  createBunchOfKey(): void {
    if (this.createBunchOfKeyModalForm.valid) {
      this.bunchOfKeysService.createBunchOfKey(this.createBunchOfKeyModalForm.value.name ?? '', this.createBunchOfKeyModalForm.value.description ?? '').subscribe({
        next: (bunchOfKey) => {
          console.log('New bunch of key added:', bunchOfKey);
          this.bunchOfKeys.push(bunchOfKey);
          this.createBunchOfKeyModalForm.reset();
        },
        error: (err) => {
          console.error('Error adding new bunch of key:', err);
        }
      });
    }
  }
}
