# Test Payment Functionality

|ID          |
|------------|
|WSTG-BUSL-10|

## Summary

TODO

## Test Objectives

- TODO

## How to Test

### Quantity Tampering

- Can you add negative numbers of items to to your basket?
    - If the total has to be positive, can you add some negative values to reduce it?
- Can you add non-integer numbers of items?
- If quality values are from a dropdown, can you tamper to use other ones?

### Price Tampering

#### On the Application

- Editing HTML forms/intercepting on application
- If there are multiple types of items, do they follow the same rules?
    - For example, can a negative donation be added to the checkout process to reduce the total?

#### On the Payment Gateway

- Editing HTML or intercepting on transfer to payment gateway
- Negative transactions may be processed as a refund

#### Encrypted Transaction Details

In order to prevent the transaction being tampered with, some payment gateways will encrypt the details of the request that is made to them. For example, [Paypal](https://developer.paypal.com/api/nvp-soap/paypal-payments-standard/integration-guide/encryptedwebpayments/#link-usingewptoprotectmanuallycreatedpaymentbuttons) do this using public key cryptography.

The first thing to try is making an unencrypted request, as some payment gateways allow insecure transactions unless a specific configuration option has been set.

If this doesn't work, then you need to find the public key that is used to encrypt the transaction details, which could be exposed in a backup of the application, or if you can find a directory traversal vulnerability.

Alternatively, it's possible that the application re-uses the same public/private key pair for the payment gateway and it's digital certificate. You can obtain the public key from the server with the following command:

```bash
echo -e '\0' | openssl s_client -connect example.org:443 2>/dev/null | openssl x509 -pubkey -noout
```

Once you have this key, you can then try and create an encrypted request (based on the payment gateway's documentation), and submit it to the gateway to see if it's accepted.

#### Secure Hashes

Other payment gateway use a secure hash (or HMAC) of the transaction details to prevent tampering. The exact details of how this is done will vary between providers (for example, [Adyen](https://docs.adyen.com/online-payments/classic-integrations/hosted-payment-pages/hmac-signature-calculation) use HMAC-SHA256), but it will normally include the details of the transaction and a secret value. For example, a hash may be calculated as:

```php
$secure_hash = md5($merchant_id . $transaction_id . $items . $total_value . $secret)
```

This value is then added to the POST request that is sent to the payment gateway, and verified to ensure that the transaction hasn't been tampered with.

The first thing to try is removing the secure hash, as some payment gateways allow insecure transactions unless a specific configuration option has been set.

The POST request should contain all of the values required to calculate this hash, other than the secret key. As such, if you know how the hash is calculated (which should be included in the payment gateway's documentation), then you can attempt to brute-force the secret. Alternatively, if the website is running an off-the-shelf application, there may be a default secret in the configuration files or source code. Alternatively, if you can find a backup of the website, or otherwise gain access to the configuration files, you may be able to find the secret there.

If you can obtain this secret, you can then tamper the transaction details, and then generate your own secure hash which will be accepted by the payment gateway.

#### Currency Tampering

- If you can't tamper price, can you change the currency (pay $10 when it should be £10)

#### Time Delayed Requests

- If the value of an item changes (such as on a currency exchange), can you "freeze" a request and pay with old value?

### Discount Codes

- Can you guess (TEST, SORRY, SORRY10, etc) or brute-force discount codes?
- Can you use wildcards (`%`, `*`)?
- Can you apply multiple discount codes?
- Are codes exposed it hidden `<input>` fields or HTML comments?

### Breaking Payment Flows

- Many payment flows include redirection:
    - Checkout on application
    - Redirected to third-party to make payment
    - Redirected back to `success.php` or `fail.php` depending on status
- Can you get redirected, then force-browse to success page?
- Can you make multiple requests to success page?
- Does success page include an ID? IDOR

### Exploiting Transaction Processing Fees

- Merchants have to pay fees for every transaction processed
    - Usually fixed fee + percentage
- Very small transaction ($0.01) usually cost merchant money to receive
- Check minimum transaction values

### Testing Logistics

- If testing in live, may result in real transactions
- Get client to cancel and refund (processing fees?)
- If testing in dev/staging, get test payment cards
- Keep careful track of any transactions made

### PCI DSS

- Standard that covers card payments
- Any application taking payments should be compliant
- Requirements depend on how payments are made (see [Visa Guidance](https://www.visa.co.uk/dam/VCOM/regional/ve/unitedkingdom/PDF/risk/processing-e-commerce-payments-guide-73-17337.pdf)):
    - SAQ A: redirect or IFRAME
    - SAQ A-EP: cross-domain POST
    - SAQ D: cardholder data touches server
- SAQ A is best choice, should flag clients not doing that
- Flag if cardholder data is stored and can be viewed/retrieved

### Test Payment Cards

- Most payment gateways have test cards - can these be used?
    - [Adyen](https://docs.adyen.com/development-resources/test-cards/test-card-numbers)
    - [Globalpay](https://developer.globalpay.com/resources/test-card-numbers)
    - [Stripe](https://stripe.com/docs/testing)
    - [Worldpay](http://support.worldpay.com/support/kb/bg/testandgolive/tgl5103.html)

## Related Test Cases

- TODO

## Remediation

- Use a redirect or IFRAME wherever possible.
- Handle all payment information on server-side:
    - Only things client-side should be item ID and quantity
- Review payment gateway documentation and use all available security features
- Ensure that application payment flow is robust

## Tools

- Intercepting proxy

## References

- TODO
