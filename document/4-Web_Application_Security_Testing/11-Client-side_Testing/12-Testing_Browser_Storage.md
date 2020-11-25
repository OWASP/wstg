# Testing Browser Storage

|ID          |
|------------|
|WSTG-CLNT-12|

## Summary

Browsers provide the following client-side storage mechanisms for developers to store and retrieve data:

- Local Storage
- Session Storage
- IndexedDB
- Web SQL (Deprecated)
- Cookies

These storage mechanisms can be viewed and edited using the browser's developer tools, such as [Google Chrome DevTools](https://developers.google.com/web/tools/chrome-devtools/storage/localstorage) or [Firefox's Storage Inspector](https://developer.mozilla.org/en-US/docs/Tools/Storage_Inspector).

Note: While cache is also a form of storage it is covered in a [separate section](../04-Authentication_Testing/06-Testing_for_Browser_Cache_Weaknesses.md) covering its own peculiarities and concerns.

## Test Objectives

- Determine whether the website is storing sensitive data in client-side storage.
- The code handling of the storage objects should be examined for possibilities of injection attacks, such as utilizing unvalidated input or vulnerable libraries.

## How to Test

### Local Storage

`window.localStorage` is a global property that implements the [Web Storage API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Storage_API) and provides **persistent** key-value storage in the browser.

Both the keys and values can only be strings, so any non-string values must be converted to strings first before storing them, usually done via [JSON.stringify](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/JSON/stringify).

Entries to `localStorage` persist even when the browser window closes, with the exception of windows in Private/Incognito mode.

The maximum storage capacity of `localStorage` varies between browsers.

#### List All Key-Value Entries

```javascript
for (let i = 0; i < localStorage.length; i++) {
  const key = localStorage.key(i);
  const value = localStorage.getItem(key);
  console.log(`${key}: ${value}`);
}
```

### Session Storage

`window.sessionStorage` is a global property that implements the [Web Storage API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Storage_API) and provides **ephemeral** key-value storage in the browser.

Both the keys and values can only be strings, so any non-string values must be converted to strings first before storing them, usually done via [JSON.stringify](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/JSON/stringify).

Entries to `sessionStorage` are ephemeral because they are cleared when the browser tab/window is closed.

The maximum storage capacity of `sessionStorage` varies between browsers.

#### List All Key-Value Entries

```javascript
for (let i = 0; i < sessionStorage.length; i++) {
  const key = sessionStorage.key(i);
  const value = sessionStorage.getItem(key);
  console.log(`${key}: ${value}`);
}
```

### IndexedDB

IndexedDB is a transactional, object-oriented database intended for structured data. An IndexedDB database can have multiple object stores and each object store can have multiple objects.

In contrast to Local Storage and Session Storage, IndexedDB can store more than just strings. Any objects supported by the [structured clone algorithm](https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API/Structured_clone_algorithm) can be stored in IndexedDB.

An example of a complex JavaScript object that can be stored in IndexedDB, but not in Local/Session Storage are [CryptoKeys](https://developer.mozilla.org/en-US/docs/Web/API/CryptoKey).

W3C recommendation on [Web Crypto API](https://www.w3.org/TR/WebCryptoAPI/) [recommends](https://www.w3.org/TR/WebCryptoAPI/#concepts-key-storage) that CryptoKeys that need to be persisted in the browser, to be stored in IndexedDB. When testing a web page, look for any CryptoKeys in IndexedDB and check if they are set as `extractable: true` when they should have been set to `extractable: false` (i.e. ensure the underlying private key material is never exposed during cryptographic operations.)

#### Print All the Contents of IndexedDB

```javascript
const dumpIndexedDB = dbName => {
  const DB_VERSION = 1;
  const req = indexedDB.open(dbName, DB_VERSION);
  req.onsuccess = function() {
    const db = req.result;
    const objectStoreNames = db.objectStoreNames || [];

    console.log(`[*] Database: ${dbName}`);

    Array.from(objectStoreNames).forEach(storeName => {
      const txn = db.transaction(storeName, 'readonly');
      const objectStore = txn.objectStore(storeName);

      console.log(`\t[+] ObjectStore: ${storeName}`);

      // Print all entries in objectStore with name `storeName`
      objectStore.getAll().onsuccess = event => {
        const items = event.target.result || [];
        items.forEach(item => console.log(`\t\t[-] `, item));
      };
    });
  };
};

indexedDB.databases().then(dbs => dbs.forEach(db => dumpIndexedDB(db.name)));
```

### Web SQL

Web SQL is deprecated since November 18, 2010 and it's recommended that web developers do not use it.

### Cookies

Cookies are a key-value storage mechanism that is primarily used for session management but web developers can still use it to store arbitrary string data.

Cookies are covered extensively in the [testing for Cookies attributes](../06-Session_Management_Testing/02-Testing_for_Cookies_Attributes.md) scenario.

#### List All Cookies

```javascript
console.log(window.document.cookie);
```

### Global Window Object

Sometimes web developers initialize and maintain global state that is available only during the runtime life of the page by assigning custom attributes to the global `window` object. For example:

```javascript
window.MY_STATE = {
  counter: 0,
  flag: false,
};
```

Any data attached on the `window` object will be lost when the page is refreshed or closed.

#### List All Entries on the Window Object

```javascript
(() => {
  // create an iframe and append to body to load a clean window object
  const iframe = document.createElement('iframe');
  iframe.style.display = 'none';
  document.body.appendChild(iframe);

  // get the current list of properties on window
  const currentWindow = Object.getOwnPropertyNames(window);

  // filter the list against the properties that exist in the clean window
  const results = currentWindow.filter(
    prop => !iframe.contentWindow.hasOwnProperty(prop)
  );

  // remove iframe
  document.body.removeChild(iframe);

  // log key-value entries that are different
  results.forEach(key => console.log(`${key}: ${window[key]}`));
})();
```

_(Modified version of this [snippet](https://stackoverflow.com/a/17246535/3099132))_

### Attack Chain

Following the identification any of the above attack vectors, an attack chain can be formed with different types of client-side attacks, such as [DOM based XSS](01-Testing_for_DOM-based_Cross_Site_Scripting.md) attacks.

## Remediation

Applications should be storing sensitive data on the server-side, and not on the client-side, in a secured manner following best practices.

## References

- [Local Storage](https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage)
- [Session Storage](https://developer.mozilla.org/en-US/docs/Web/API/Window/sessionStorage)
- [IndexedDB](https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API)
- [Web Crypto API: Key Storage](https://www.w3.org/TR/WebCryptoAPI/#concepts-key-storage)
- [Web SQL](https://www.w3.org/TR/webdatabase/)
- [Cookies](https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies)

For more OWASP resources on the HTML5 Web Storage API, see the [Session Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html#html5-web-storage-api).
