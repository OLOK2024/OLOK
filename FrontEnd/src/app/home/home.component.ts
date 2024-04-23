import { Component, OnInit } from '@angular/core';
import {RouterLink} from "@angular/router";
import {KeyService} from "../key.service";
import {NgForOf} from "@angular/common";
import { ReactiveFormsModule, FormGroup, FormControl } from '@angular/forms';
import { BunchOfKeysService } from '../bunch-of-keys.service';
import { CommonModule } from "@angular/common";
import { Router } from "@angular/router";

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
  bunchOfKeys: any[] = [];
  bunchOfKeyToUpdate: any = null;
  selectedBunchOfKeyId: string = 'all';
  addKeyForm = new FormGroup({
    domain: new FormControl('', []),
    username: new FormControl('', []),
    password: new FormControl('', []),
    bunchOfKeysId: new FormControl('', []),
  });
  createBunchOfKeyModalForm = new FormGroup({
    name: new FormControl('', []),
    description: new FormControl('', []),
  });
  updateBunchOfKeyModalForm = new FormGroup({
    name: new FormControl('', []),
    description: new FormControl('', []),
  });

  constructor(
    private keyService: KeyService,
    private bunchOfKeysService: BunchOfKeysService,
    private router: Router
  ) { }

  ngOnInit(): void {
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

  getPassword(keyId: string): void {
    for (let bunchOfKey of this.bunchOfKeys[0]) {
      for (let key of bunchOfKey.keys) {
        if (key.keyId == keyId) {
          alert(bunchOfKey.bunchOfKeysId);
          this.keyService.getPassword(bunchOfKey.bunchOfKeysId, keyId).subscribe({
            next: (password) => {
              navigator.clipboard.writeText(password.password).then(() => {
                console.log('Password copied to clipboard:', password.password);
              });
            },
            error: (err) => {
              console.error('Error fetching password:', err);
            }
          });

        }
      }
    }
  }

  logout(): void {
    localStorage.removeItem('token');
    //renvoie vers la page de login
    this.router.navigate(['/login']);
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
  selectBunchOfKeyForUpdate(bunchOfKey: any) {
    this.bunchOfKeyToUpdate = bunchOfKey[0];
    this.updateBunchOfKeyModalForm.patchValue({
      name: bunchOfKey[0].name,
      description: bunchOfKey[0].description,
    });
  }
  updateBunchOfKey(): void {
    if (this.updateBunchOfKeyModalForm.valid) {
      this.bunchOfKeysService.updateBunchOfKey(this.updateBunchOfKeyModalForm.value.name ?? '', this.updateBunchOfKeyModalForm.value.description ?? '', this.bunchOfKeyToUpdate.bunchOfKeysId).subscribe({
        next: (updatedBunchOfKey) => {
          console.log('Bunch of key updated:', updatedBunchOfKey);
          const index = this.bunchOfKeys.findIndex((bunch) => bunch[0].bunchOfKeysId === updatedBunchOfKey.bunchOfKeysId);
          this.bunchOfKeys[index] = [updatedBunchOfKey];
          //this.updateBunchOfKeyModalForm.reset();
          this.bunchOfKeyToUpdate = null;
        },
        error: (err) => {
          console.error('Error updating bunch of key:', err);
        }
      });
    }
  }
  deleteBunchOfKey(bunchOfKey: any): void {
    if (confirm('Are you sure you want to delete this bunch of key?')) {
      console.log('Deleting bunch of key:', bunchOfKey.bunchOfKeysId);
      this.bunchOfKeysService.deleteBunchOfKey(bunchOfKey.bunchOfKeysId, false).subscribe({
        next: () => {
          console.log('Bunch of key deleted:', bunchOfKey);
          const index = this.bunchOfKeys.findIndex((bunch) => bunch.bunchOfKeysId === bunchOfKey.bunchOfKeysId);
          this.bunchOfKeys.splice(index, 1);
          this.bunchOfKeyToUpdate = null;
        },
        error: (err) => {
          console.error('Error deleting bunch of key:', err);
        }
      });
    }
  }
  filterBunchOfKeySelected(bunchOfKeyId: string) {
    this.selectedBunchOfKeyId = bunchOfKeyId;
  }
}
