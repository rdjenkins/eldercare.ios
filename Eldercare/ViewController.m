//
//  ViewController.m
//  Eldercare
//
//  Created by Dean Jenkins on 21/10/2017.
//  Copyright © 2017 Dean Jenkins. All rights reserved.
//

#import "ViewController.h"

@interface ViewController ()

@property (strong, nonatomic) IBOutlet UIWebView *webView;

@end

@implementation ViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    // Do any additional setup after loading the view, typically from a nib.
    
    _webView.delegate = self; // this line required to make the link capture for http below work!
    
    NSBundle *mainBundle = [NSBundle mainBundle];
    
    NSURL *homeIndexUrl = [mainBundle URLForResource:@"eldercare-master/index" withExtension:@"html"];
    
    NSURLRequest *urlReq = [NSURLRequest requestWithURL:homeIndexUrl];
    
    [self.webView loadRequest:urlReq];
    
}


- (void)didReceiveMemoryWarning {
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

// Capture links
// adapted heavily from http://stackoverflow.com/questions/37248767/objective-c-open-links-outside-uiwebview
- (BOOL) webView:(UIWebView *)webView shouldStartLoadWithRequest:(NSURLRequest *)request navigationType:(UIWebViewNavigationType)navigationType
{
    if (navigationType == UIWebViewNavigationTypeLinkClicked ) { // user clicked something
        if (![request.URL.path containsString:@"eldercare-master"]) { // an external website
            NSLog(@"external Link clicked");
            if ([[UIApplication sharedApplication] canOpenURL:[NSURL URLWithString:@"http://"]]) { // is this check necessary?
                NSLog(@"Opening link in shared App (probably Safari)");
                [[UIApplication sharedApplication] openURL:request.URL];
            }
            else {
                //                    [[UIApplication sharedApplication] openURL:request.URL];
                NSLog(@"No Shared APP can open the URL"); // boo hoo
            }
            //            }
            return NO; // Don't go there in webView so that we don't confuse things.
        }
        else {
            NSLog(@"within-app link clicked");
        }
        
    }
    return YES; // assume yes!
}

@end
