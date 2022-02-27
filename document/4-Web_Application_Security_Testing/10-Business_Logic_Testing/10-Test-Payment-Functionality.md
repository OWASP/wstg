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
- Can you add non-integer numbers of items?
- If quality values are from a dropdown, can you tamper to use other ones?

### Price Tampering

#### On the Application

- Editing HTML forms/intercepting on application

#### On the Payment Gateway

- Editing HTML or intercepting on transfer to payment gateway
- Negative transactions may be processed as a refund

#### Secure Hashes

- Some payment gateways use secure hashes to prevent tampering
- Check that secure hash is actually enforced - try removing it
- Can be based on public/private key crypto (such as [PayPal](https://developer.paypal.com/api/nvp-soap/paypal-payments-standard/integration-guide/encryptedwebpayments/#link-usingewptoprotectmanuallycreatedpaymentbuttons))
    - Try using public key from certificate
- Can be bashed on a secret key (such as Adyen, which uses [HMAC-SHA256](https://docs.adyen.com/online-payments/classic-integrations/hosted-payment-pages/hmac-signature-calculation))
    - Try and guess or brute-force

#### Currency Tampering

- If you can't tamper price, can you change the currency (pay $10 when it should be £10)

#### Time Delayed Requests

- If the value of an item changes (such as on a currency exchange), can you "freeze" a request and pay with old value?

### Discount Codes

- Can you guess (TEST, SORRY, SORRY10, etc) or brute-force discount codes?
- Can you use wildcards (`%`, `*`)?
- Can you apply multiple discount codes?

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
