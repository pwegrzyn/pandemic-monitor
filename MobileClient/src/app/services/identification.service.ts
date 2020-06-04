import { Injectable } from '@angular/core';
import { Plugins, FilesystemDirectory, FilesystemEncoding } from '@capacitor/core';
import { Storage } from '@ionic/storage';
import { Observable, of, from } from 'rxjs';

const { Filesystem } = Plugins;


@Injectable({
  providedIn: 'root'
})
export class IdentificationService {

  private currentIdentity: Identity;
  private idKey = "identity_number";

  constructor(private storage: Storage) { }

  public getIdentity(): Observable<number> {
    if (this.currentIdentity != null) {
      console.log("Using in-memory Identity...");
      return of(this.currentIdentity.idNumber);
    }
    return from(this.storage.get(this.idKey).then((val) => {
      if (!val) {
        console.log("Could not get saved identity, creating new one...");
        const newIdentityNumber = this.getRandomInt(1000000000);
        this.currentIdentity = {storageKey: this.idKey, filePath: null, idNumber: newIdentityNumber};
        this.saveIdentityStorage(this.currentIdentity);
        return this.currentIdentity.idNumber;
      } else {
        console.log("Using file system Identity...")
        this.currentIdentity = {storageKey: this.idKey, filePath: null, idNumber: val};
        return this.currentIdentity.idNumber;
      }
    }, (err) => {
      console.log("There was an error when getting the saved data, creating new one...");
      const newIdentityNumber = this.getRandomInt(1000000000);
      this.currentIdentity = {storageKey: this.idKey, filePath: null, idNumber: newIdentityNumber};
      this.saveIdentityStorage(this.currentIdentity);
      return this.currentIdentity.idNumber;
    }));
  }

  private async saveIdentityStorage(identity: Identity) {
    return this.storage.set(identity.storageKey, identity.idNumber);
  }

  private async saveIdentityFS(identity: Identity) {
    const fileName = new Date().getTime() + "_PC_identity.txt";
    identity.filePath = fileName;
    const savedFile = await Filesystem.writeFile({
      path: fileName,
      data: identity.idNumber.toString(),
      directory: FilesystemDirectory.Data
    });
    return savedFile;
  }

  async fileRead(filePath) {
    let contents = await Filesystem.readFile({
      path: filePath,
      directory: FilesystemDirectory.Documents,
      encoding: FilesystemEncoding.UTF8
    });
    return contents;
  }

  private getRandomInt(max: number): number {
    return Math.floor(Math.random() * Math.floor(max));
  }
}

interface Identity {
  storageKey: string;
  filePath: string;
  idNumber: number;
}