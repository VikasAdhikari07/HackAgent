import Header from "@/components/Header";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { MessageCircle } from "lucide-react";

export default function Contact() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-purple-50">
      <Header />
      
      <div className="container mx-auto px-4 py-16 max-w-4xl">
        <Card className="border-0 shadow-lg bg-white/80 backdrop-blur-sm">
          <CardContent className="p-12 text-center">
            <h1 className="text-3xl font-bold text-gray-900 mb-6">
              Contact Us
            </h1>
            <div className="space-y-6 text-gray-600 max-w-2xl mx-auto">
              <p className="text-lg">
                This page is currently a placeholder. The full Contact page content is not yet implemented.
              </p>
              <p>
                To continue building this page with contact forms, support information, or team details, 
                please provide additional specifications for what you'd like to include here.
              </p>
              <div className="pt-6">
                <Button className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700">
                  <MessageCircle className="h-4 w-4 mr-2" />
                  Continue Prompting to Build This Page
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
